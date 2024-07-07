document.addEventListener("DOMContentLoaded", (event) => {
  var socket = io.connect("http://" + document.domain + ":" + location.port);

  document
    .getElementById("start-binary-clock")
    .addEventListener("click", () => {
      socket.emit("start_routine", "binary_clock");
    });

  document.getElementById("start-sweep").addEventListener("click", () => {
    socket.emit("start_routine", "sweep");
  });

  document.getElementById("stop-routine").addEventListener("click", () => {
    socket.emit("stop_routine");
  });
});
