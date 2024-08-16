navigator.bluetooth.requestDevice(
  {
    filters: [{ name: 'WalkingPad' }]
  })
.then(device => {
  console.log(device.name);
  return device.gatt.connect();
})
.then(server => {
  // Interact with the device's GATT server
})
.catch(error => {
  console.log(error);
});