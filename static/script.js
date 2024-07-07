document.addEventListener("DOMContentLoaded", (event) => {
  const binaryClockButton = document.getElementById("start-binary-clock");
  const sweepButton = document.getElementById("start-sweep");
  const bounceButton = document.getElementById("start-bounce");
  const resetButton = document.getElementById("stop-routine");
  const runningIcon = document.getElementById("runningIcon");
  const zeroPairButton = document.getElementById("zero-pair");

  function updateUI(status) {
    if (status === "running") {
      binaryClockButton.disabled = true;
      sweepButton.disabled = true;
      bounceButton.disabled = true;
      zeroPairButton.disabled = true;
      runningIcon.style.display = "block"; // Show running icon
    } else {
      binaryClockButton.disabled = false;
      sweepButton.disabled = false;
      bounceButton.disabled = false;
      zeroPairButton.disabled = false;
      runningIcon.style.display = "none"; // Hide running icon
    }
  }

  // Button event listeners
  binaryClockButton.addEventListener("click", () => {
    fetch("/start_binary_clock")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(() => updateUI("running"))
      .catch((err) => console.error(err));
  });

  sweepButton.addEventListener("click", () => {
    fetch("/start_sweep")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(() => updateUI("running"))
      .catch((err) => console.error(err));
  });

  bounceButton.addEventListener("click", () => {
    fetch("/start_bounce")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(() => updateUI("running"))
      .catch((err) => console.error(err));
  });

  resetButton.addEventListener("click", () => {
    fetch("/stop_routine")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(() => updateUI("idle"))
      .catch((err) => console.error(err));
  });
});
