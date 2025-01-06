document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("pre").forEach((block) => {
    hljs.highlightElement(block);
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const codeSnippets = document.querySelectorAll(".code-snippet");

  codeSnippets.forEach((snippet) => {
    // Wrap in <pre><code> for better rendering
    const pre = document.createElement("pre");
    const code = document.createElement("code");
    code.textContent = snippet.textContent; // Preserve original text
    pre.appendChild(code);

    snippet.replaceWith(pre); // Replace the original
  });

  // Initialize Highlight.js for syntax highlighting
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });
});

ClassicEditor.create(document.querySelector("#editor"), {
  plugins: [CodeBlock],
  toolbar: ["codeBlock", ...otherButtons],
  codeBlock: {
    languages: [
      { language: "plaintext", label: "Plain Text" },
      { language: "python", label: "Python" },
      { language: "javascript", label: "JavaScript" },
    ],
  },
});
