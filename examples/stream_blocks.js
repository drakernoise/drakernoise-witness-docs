const blurt = require('@blurtfoundation/blurtjs');

// Configure RPC Endpoint
blurt.api.setOptions({ url: 'https://rpc.drakernoise.com' });

console.log("Listening for new blocks on rpc.drakernoise.com...");

blurt.api.streamBlockNumber((err, blockNum) => {
    if (err) {
        console.error("Stream Error:", err);
        return;
    }

    console.log(`New Block: #${blockNum}`);

    // Fetch full block data (Optional)
    blurt.api.getBlock(blockNum, (err, block) => {
        if (!err && block) {
            console.log(` - Witness: ${block.witness}`);
            console.log(` - Transactions: ${block.transactions.length}`);
        }
    });
});
