import { EmailMessage } from "cloudflare:email";

const ALLOWED_ORIGINS = [
  'https://rishabhprasad.dev',
  'https://riri0410.github.io',
  'http://localhost:5173',
  'http://127.0.0.1:5500' // Local testing
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = ALLOWED_ORIGINS.includes(origin);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': allowed ? origin : '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    // Origin check
    if (!allowed && origin !== '') {
      return new Response('Forbidden', { status: 403 });
    }

    if (request.method !== 'POST') {
      return new Response('OK', { status: 200, headers: { 'Access-Control-Allow-Origin': allowed ? origin : '*' } });
    }

    try {
      const reqJson = await request.json();

      // ==========================================
      // 1. CONTACT FORM LOGIC (Web3Forms Proxy)
      // ==========================================
      if (reqJson.type === 'contact') {
        const { name, email, subject, message, turnstileToken } = reqJson;

        // Verify Cloudflare Turnstile token
        const turnstileVerify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: `secret=${env.TURNSTILE_SECRET_KEY}&response=${turnstileToken}`
        });

        const turnstileData = await turnstileVerify.json();
        
        if (!turnstileData.success) {
          return new Response(JSON.stringify({ success: false, message: 'Captcha verification failed. Are you a bot?' }), {
            status: 400,
            headers: { 'Access-Control-Allow-Origin': origin, 'Content-Type': 'application/json' }
          });
        }

        // ==========================================
        // Forward to Destination via Cloudflare Native Email
        // ==========================================
        if (!env.SEB) {
          return new Response(JSON.stringify({ 
            success: false, 
            message: "Missing 'SEB' (Send Email) binding in Cloudflare." 
          }), { status: 500, headers: { 'Access-Control-Allow-Origin': origin, 'Content-Type': 'application/json' } });
        }

        const destination = env.DESTINATION_EMAIL || 'rishabhprasad.academics@gmail.com'; 
        const sender = env.SENDER_EMAIL || 'noreply@rishabhprasad.dev'; // Must be a verified sender in Cloudflare

        // Construct raw RFC 5322 MIME string manually
        const rawEmail = `From: "Portfolio Contact Form" <${sender}>\r\n` +
                         `To: <${destination}>\r\n` +
                         `Reply-To: <${email}>\r\n` +
                         `Subject: New Portfolio Message from ${name}: ${subject}\r\n` +
                         `Content-Type: text/plain; charset="utf-8"\r\n\r\n` +
                         `Name: ${name}\r\n` +
                         `Email: ${email}\r\n\r\n` +
                         `Message:\r\n${message}\r\n`;

        try {
          const emailMsg = new EmailMessage(sender, destination, rawEmail);
          await env.SEB.send(emailMsg);
          
          return new Response(JSON.stringify({ success: true, message: "Email natively dispatched." }), {
            headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': origin }
          });
        } catch (e) {
          return new Response(JSON.stringify({ success: false, message: "Cloudflare Email Failed: " + e.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': origin }
          });
        }
      }

      // ==========================================
      // 2. CHATBOT LOGIC (LLaMA 3.1)
      // ==========================================
      const { contents, system_instruction } = reqJson;
      const messages = [];

      if (system_instruction?.parts?.[0]?.text) {
        messages.push({ role: 'system', content: system_instruction.parts[0].text });
      }

      if (contents && Array.isArray(contents)) {
        contents.forEach(c => {
          messages.push({
            role: c.role === 'model' ? 'assistant' : 'user',
            content: c.parts[0].text
          });
        });
      }

      const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages });

      return new Response(JSON.stringify({
        candidates: [{ content: { parts: [{ text: response.response }] } }]
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': origin,
        }
      });
      
    } catch (error) {
       return new Response(JSON.stringify({ success: false, message: error.toString() }), {
         status: 500,
         headers: { 'Access-Control-Allow-Origin': origin, 'Content-Type': 'application/json' }
       });
    }
  }
};
