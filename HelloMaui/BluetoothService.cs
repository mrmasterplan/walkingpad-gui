using InTheHand.Bluetooth;
using System;
using System.Threading.Tasks;
using System.Diagnostics;

public class BluetoothService
{
    private BluetoothDevice _device;

    public async Task<BluetoothDevice> FindDeviceAsync(string deviceName)
    {
        var devices = await Bluetooth.ScanForDevicesAsync();

        foreach (var device in devices)
        {
            Debug.WriteLine($"Found device: {device.Name} (Address: {device.Id})");
        }

        _device = devices.FirstOrDefault(d => d.Name == deviceName);

        if (_device == null)
        {
            throw new Exception("Device not found.");
        }

        return _device;
    }
}
