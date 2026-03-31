// Set REPLICATE_TOKEN as a secret in your Cloudflare Worker:
// wrangler secret put REPLICATE_TOKEN
const PROMPT = 'Change only the smile area. Give this person a perfect confident smile with straight aligned bright white teeth, fully visible upper teeth, minimal gum show, natural tooth shapes and realistic enamel texture. Smile width should fit this face naturally. Keep face, skin, eyes, hair, jawline, background and lighting identical.';
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request, env) {
    const REPLICATE_TOKEN = env.REPLICATE_TOKEN;
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS });
    }
    if (request.method !== 'POST') {
      return json({ error: 'Method not allowed' }, 405);
    }
    try {
      const body = await request.json();
      const { image } = body;
      if (!image) return json({ error: 'No image provided' }, 400);

      const payloadKB = Math.round(image.length / 1024);
      console.log(`Received image payload: ${payloadKB} KB`);

      const createRes = await fetch(
        'https://api.replicate.com/v1/models/google/nano-banana/predictions',
        {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + REPLICATE_TOKEN,
            'Content-Type': 'application/json',
            'Prefer': 'wait=60',
          },
          body: JSON.stringify({
            input: {
              prompt: PROMPT,
              image: image,
              aspect_ratio: 'match_input_image',
              output_format: 'jpg',
            },
          }),
        }
      );

      if (!createRes.ok) {
        const errText = await createRes.text();
        console.error('Replicate API error:', createRes.status, errText);
        return json({ error: 'Replicate API error', status: createRes.status, detail: errText }, 502);
      }

      const prediction = await createRes.json();

      if (prediction.status === 'succeeded' && prediction.output) {
        const url = Array.isArray(prediction.output) ? prediction.output[0] : prediction.output;
        return json({ processedImageUrl: url });
      }

      if (prediction.status === 'failed') {
        return json({ error: 'Prediction failed', detail: prediction.error }, 500);
      }

      const id = prediction.id;
      if (!id) return json({ error: 'No prediction ID returned', detail: prediction }, 500);

      for (let i = 0; i < 30; i++) {
        await sleep(2000);
        const pollRes = await fetch('https://api.replicate.com/v1/predictions/' + id, {
          headers: { 'Authorization': 'Bearer ' + REPLICATE_TOKEN },
        });
        const poll = await pollRes.json();

        if (poll.status === 'succeeded' && poll.output) {
          const url = Array.isArray(poll.output) ? poll.output[0] : poll.output;
          return json({ processedImageUrl: url });
        }
        if (poll.status === 'failed' || poll.status === 'canceled') {
          return json({ error: 'Prediction ' + poll.status, detail: poll.error }, 500);
        }
      }
      return json({ error: 'Timeout waiting for prediction' }, 504);
    } catch (err) {
      console.error('Worker error:', err.message, err.stack);
      return json({ error: err.message }, 500);
    }
  }
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}
