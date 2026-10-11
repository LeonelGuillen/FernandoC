// Cloudflare Pages Function — POST /api/contact
// Variables de entorno (Pages > Settings > Variables and Secrets):
//   RESEND_API_KEY   (secreto)  API key de https://resend.com
//   CONTACT_TO                  correo que recibe los mensajes
//   CONTACT_FROM                remitente verificado en Resend, p. ej. "Sitio web <web@fernandocastillocr.com>"
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

  if (!env.RESEND_API_KEY || !env.CONTACT_TO || !env.CONTACT_FROM) {
    return json({ ok: false, error: 'El formulario aún no está configurado. Intente más tarde.' }, 503);
  }

  const html = `<h2>Nuevo mensaje desde el sitio web</h2>
<p><b>Nombre:</b> ${esc(nombre)}<br><b>Correo:</b> ${esc(correo)}<br><b>Institución:</b> ${esc(institucion) || '—'}<br><b>Asunto:</b> ${esc(asunto)}</p>
<p style="white-space:pre-wrap">${esc(mensaje)}</p>`;

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: env.CONTACT_FROM, to: env.CONTACT_TO.split(',').map(s => s.trim()), reply_to: correo, subject: `[Web] ${asunto || 'Contacto'} — ${nombre}`, html })
  });
  if (!r.ok) return json({ ok: false, error: 'No fue posible enviar el mensaje en este momento.' }, 502);
  return json({ ok: true });
}

export const onRequestGet = () => json({ ok: false, error: 'Método no permitido.' }, 405);
