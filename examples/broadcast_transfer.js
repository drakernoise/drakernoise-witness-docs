const blurt = require('@blurtfoundation/blurtjs');

// Configure RPC Endpoint
blurt.api.setOptions({ url: 'https://rpc.drakernoise.com' });

const ACTIVE_KEY = 'YOUR_PRIVATE_ACTIVE_KEY'; // CAUTION: Never commit real keys
const USERNAME = 'your_username';

function sendTransfer() {
    const wif = ACTIVE_KEY;
    const from = USERNAME;
    const to = 'drakernoise';
    const amount = '1.000 BLURT';
    const memo = 'Donation for Witness service';

    console.log(`Sending ${amount} to ${to}...`);

    blurt.broadcast.transfer(wif, from, to, amount, memo, (err, result) => {
        if (err) {
            console.error("Broadcast Failed:", err);
        } else {
            console.log("Success! Transaction ID:", result.id);
            console.log("Block:", result.block_num);
        }
    });
}

// sendTransfer(); // Uncomment to run
