document.addEventListener("DOMContentLoaded", () => {
  // Handle domain registration form
  const registerForm = document.getElementById("registerForm")
  const registerResult = document.getElementById("registerResult")

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const domain = document.getElementById("domain").value.trim()

      // Simple domain validation
      const domainPattern = /^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$/
      if (!domainPattern.test(domain)) {
        showResult("Please enter a valid domain name (e.g., example.com)", "error")
        return
      }

      // Send registration request
      fetch("/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.detail) {
            // Error response
            showResult(data.detail, "error")
          } else {
            // Success response
            showResult(
              `
                        <h4>Registration Successful!</h4>
                        <p><strong>Domain:</strong> ${data.domain}</p>
                        <p><strong>API Key:</strong> ${data.api_key}</p>
                        <p>Save this API key! You'll need it to track visits.</p>
                        <p><a href="/dashboard/${data.api_key}" class="btn primary">Go to Dashboard</a></p>
                    `,
              "success",
            )
          }
        })
        .catch((error) => {
          showResult("An error occurred. Please try again.", "error")
          console.error("Error:", error)
        })
    })
  }

  // Helper function to show result message
  function showResult(message, type) {
    registerResult.innerHTML = message
    registerResult.classList.remove("hidden", "success", "error")
    registerResult.classList.add(type)
  }
})
