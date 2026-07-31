export async function detectLanguage(text) {
  const response = await fetch("http://localhost:5800/detect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });

  const data = await response.json();
  return data.language;
}
