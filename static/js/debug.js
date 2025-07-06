document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("generateBtn").addEventListener("click", async () => {
    try {
      const response = await fetch("/debug-meal-plan")
      const data = await response.json()
      document.querySelector("#result pre").textContent = JSON.stringify(data, null, 2)
    } catch (error) {
      document.querySelector("#result pre").textContent = "Error: " + error.message
    }
  })

  document.getElementById("checkSessionBtn").addEventListener("click", async () => {
    try {
      const response = await fetch("/api/check-session")
      const data = await response.json()
      document.querySelector("#result pre").textContent = JSON.stringify(data, null, 2)
    } catch (error) {
      document.querySelector("#result pre").textContent = "Error: " + error.message
    }
  })

  document.getElementById("clearSessionBtn").addEventListener("click", async () => {
    try {
      const response = await fetch("/api/clear-session")
      const data = await response.json()
      document.querySelector("#result pre").textContent = JSON.stringify(data, null, 2)
    } catch (error) {
      document.querySelector("#result pre").textContent = "Error: " + error.message
    }
  })
})

