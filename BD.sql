-- 1. Crear la tabla principal: subscriptions
CREATE TABLE IF NOT EXISTS public.subscriptions (
  user_id TEXT PRIMARY KEY,                -- pedido por la prueba
  email TEXT NOT NULL,
  plan_type TEXT NOT NULL CHECK (plan_type IN ('basic','pro')),
  status TEXT NOT NULL CHECK (status IN ('trial','active','past_due','canceled')),
  trial_ends_at TIMESTAMPTZ,
  next_billing_at TIMESTAMPTZ,
  last_payment_attempt TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Índices que ayudan a las consultas por fecha / estado
CREATE INDEX IF NOT EXISTS idx_subscriptions_next_billing_at ON public.subscriptions (next_billing_at);
CREATE INDEX IF NOT EXISTS idx_subscriptions_trial_ends_at ON public.subscriptions (trial_ends_at);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON public.subscriptions (status);

-- 3. Tabla para logs de automatización (automation_logs)
CREATE TABLE IF NOT EXISTS public.automation_logs (
  id SERIAL PRIMARY KEY,
  user_id TEXT,
  action TEXT,
  error_message TEXT,
  metadata JSONB,            -- opcional: datos extra
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION public.trigger_set_timestamp()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at := NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS subscriptions_set_timestamp ON public.subscriptions;
CREATE TRIGGER subscriptions_set_timestamp
BEFORE UPDATE ON public.subscriptions
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();

-- 5. Función auxiliar: avanzar next_billing_at + 1 mes de forma segura (simula la actualización transaccional)
CREATE OR REPLACE FUNCTION public.advance_billing_one_month(p_user_id TEXT)
RETURNS TABLE(success BOOLEAN, message TEXT) AS $$
DECLARE
  cur_next TIMESTAMPTZ;
BEGIN
  SELECT next_billing_at INTO cur_next FROM public.subscriptions WHERE user_id = p_user_id FOR UPDATE;
  IF NOT FOUND THEN
    RETURN QUERY SELECT FALSE, 'user not found';
    RETURN;
  END IF;

  IF cur_next IS NULL THEN
    -- si no había next_billing_at, ponemos NOW()+1 month
    UPDATE public.subscriptions
      SET next_billing_at = NOW() + INTERVAL '1 month'
      WHERE user_id = p_user_id;
  ELSE
    UPDATE public.subscriptions
      SET next_billing_at = (cur_next + INTERVAL '1 month')
      WHERE user_id = p_user_id;
  END IF;

  RETURN QUERY SELECT TRUE, 'next_billing_at updated';
EXCEPTION WHEN OTHERS THEN
  RETURN QUERY SELECT FALSE, SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- 6. Vista práctica: suscripciones no canceladas (útil para n8n)
CREATE OR REPLACE VIEW public.view_active_subscriptions AS
SELECT * FROM public.subscriptions WHERE status != 'canceled';

-- 7. Datos de prueba
INSERT INTO public.subscriptions (user_id, email, plan_type, status, trial_ends_at, next_billing_at)
VALUES
  ('user_001', 'user1@example.com', 'pro', 'trial', NOW() + INTERVAL '3 days', NULL)
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO public.subscriptions (user_id, email, plan_type, status, trial_ends_at, next_billing_at)
VALUES
  ('user_002', 'user2@example.com', 'basic', 'trial', NOW(), NULL)
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO public.subscriptions (user_id, email, plan_type, status, trial_ends_at, next_billing_at)
VALUES
  ('user_003', 'user3@example.com', 'pro', 'active', NULL, NOW())
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO public.subscriptions (user_id, email, plan_type, status, trial_ends_at, next_billing_at)
VALUES
  ('user_004', 'user4@example.com', 'basic', 'past_due', NULL, NOW() - INTERVAL '2 days')
ON CONFLICT (user_id) DO NOTHING;