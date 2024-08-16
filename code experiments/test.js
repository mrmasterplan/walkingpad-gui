async function getDeviceInfo() {
    try {
        // Request a Bluetooth device with no filters to discover available services and characteristics
        const device = await navigator.bluetooth.requestDevice({
            filters: [{ name: 'WalkingPad' }],
            optionalServices:['00001800-0000-1000-8000-00805f9b34fb', '0000180a-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d1912', '0000fe00-0000-1000-8000-00805f9b34fb', '00002902-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d1912', '00002901-0000-1000-8000-00805f9b34fb', '00002a00-0000-1000-8000-00805f9b34fb', '00002a01-0000-1000-8000-00805f9b34fb', '00002a04-0000-1000-8000-00805f9b34fb', '00002a25-0000-1000-8000-00805f9b34fb', '00002a26-0000-1000-8000-00805f9b34fb', '00002a28-0000-1000-8000-00805f9b34fb', '00002a24-0000-1000-8000-00805f9b34fb', '00002a29-0000-1000-8000-00805f9b34fb', '0000fe01-0000-1000-8000-00805f9b34fb', '0000fe02-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d2b12']

        });

        // Connect to the GATT server
        const server = await device.gatt.connect();

        // Get all primary services
        const services = await server.getPrimaryServices();

        // Iterate through each service
        for (const service of services) {
            console.log(`Service: ${service.uuid}`);

            // Get characteristics for each service
            const characteristics = await service.getCharacteristics();

            // Iterate through each characteristic
            for (const characteristic of characteristics) {
                console.log(`Characteristic: ${characteristic.uuid}`);
            }
        }
    } catch (error) {
        console.error('Something went wrong:', error);
    }
}

// Call the function to execute
getDeviceInfo();



async function connectToDevice() {
    try {
        // Replace 'your-service-uuid' with the actual UUID you suspect
        const device = await navigator.bluetooth.requestDevice({
            filters: [{ name: 'WalkingPad' }],
            optionalServices:['00001800-0000-1000-8000-00805f9b34fb', '0000180a-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d1912', '0000fe00-0000-1000-8000-00805f9b34fb', '00002902-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d1912', '00002901-0000-1000-8000-00805f9b34fb', '00002a00-0000-1000-8000-00805f9b34fb', '00002a01-0000-1000-8000-00805f9b34fb', '00002a04-0000-1000-8000-00805f9b34fb', '00002a25-0000-1000-8000-00805f9b34fb', '00002a26-0000-1000-8000-00805f9b34fb', '00002a28-0000-1000-8000-00805f9b34fb', '00002a24-0000-1000-8000-00805f9b34fb', '00002a29-0000-1000-8000-00805f9b34fb', '0000fe01-0000-1000-8000-00805f9b34fb', '0000fe02-0000-1000-8000-00805f9b34fb', '00010203-0405-0607-0809-0a0b0c0d2b12']

        });

        const server = await device.gatt.connect();
        const service = await server.getPrimaryService('0000fe01-0000-1000-8000-00805f9b34fb');

        // Log the service UUID
        console.log(`Connected to service: ${service.uuid}`);

        // Get characteristics for this service
        const characteristics = await service.getCharacteristics();

        // Iterate through each characteristic
        for (const characteristic of characteristics) {
            console.log(`Characteristic: ${characteristic.uuid}`);
        }
    } catch (error) {
        console.error('Something went wrong:', error);
    }
}

// Call the function to execute
connectToDevice();
