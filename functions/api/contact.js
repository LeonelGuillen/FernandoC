// Cloudflare Pages Function — POST /api/contact
// Envía el mensaje mediante el Worker "fernandoc-mailer" (Service binding MAILER, ver wrangler.toml),
// que usa el enrutamiento de correo de Cloudflare. El correo destino es un secreto del Worker
// (CONTACT_TO) y no aparece en este repositorio.
//   TURNSTILE_SECRET (opcional) si se activa Cloudflare Turnstile en el formulario

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });

const esc = s => String(s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export async function onRequestPost({ request, env }) {
  let fd;
  try { fd = await request.formData(); } catch { return json({ ok: false, error: 'Solicitud inválida.' }, 400); }

  // Honeypot anti-spam
  if (fd.get('website')) return json({ ok: true });

  const nombre = (fd.get('nombre') || '').toString().trim().slice(0, 120);
  const correo = (fd.get('correo') || '').toString().trim().slice(0, 160);
  const institucion = (fd.get('institucion') || '').toString().trim().slice(0, 160);
  const asunto = (fd.get('asunto') || '').toString().trim().slice(0, 80);
  const mensaje = (fd.get('mensaje') || '').toString().trim().slice(0, 5000);

  if (!nombre || !mensaje || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
    return json({ ok: false, error: 'Por favor complete nombre, un correo válido y el mensaje.' }, 422);
  }

  if (env.TURNSTILE_SECRET) {
    const token = fd.get('cf-turnstile-response');
    const v = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token || '', remoteip: request.headers.get('CF-Connecting-IP') || '' })
    }).then(r => r.json()).catch(() => ({ success: false }));
    if (!v.success) return json({ ok: false, error: 'No se pudo verificar que usted no es un robot.' }, 403);
  }

  if (!env.MAILER) {
    return json({ ok: false, error: 'El formulario aún no está configurado. Intente más tarde.' }, 503);
  }

  const r = await env.MAILER.fetch('https://mailer/send', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ nombre, correo, institucion, asunto, mensaje })
  }).catch(() => null);
  if (!r || !r.ok) return json({ ok: false, error: 'No fue posible enviar el mensaje en este momento.' }, 502);
  return json({ ok: true });
}

export const onRequestGet = () => json({ ok: false, error: 'Método no permitido.' }, 405);
