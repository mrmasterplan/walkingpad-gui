namespace HelloMaui;

public partial class MainPage : ContentPage
{
	int count = 0;
    private BluetoothService _bluetoothService;

	public MainPage()
	{
		InitializeComponent();
		_bluetoothService = new BluetoothService();
	}

	private async void ConnectClicked(object sender, EventArgs e)
	{
		try
        {
            var device = await _bluetoothService.FindDeviceAsync("WalkingPad"); // Replace with your Bluetooth device name
            // Replace with the actual service and characteristic UUIDs for your device
//            var serviceUuid = new Guid("YOUR_SERVICE_UUID");
  //          var characteristicUuid = new Guid("YOUR_CHARACTERISTIC_UUID");
    //        _characteristic = await _bluluetoothService.GetCharacteristicAsync(serviceUuid, characteristicUuid);
            ResultLabel.Text = "Connected to device and characteristic found.";
        
        }
        catch (Exception ex)
        {
            ResultLabel.Text = $"Error: {ex.Message}";
        }
	}
	
	private void ModeManualClicked(object sender, EventArgs e)
	{
		count++;

		if (count == 1)
			ModeManualBtn.Text = $"Clicked {count} time";
		else
			ModeManualBtn.Text = $"Clicked {count} times";

		SemanticScreenReader.Announce(ModeManualBtn.Text);
	}
}

