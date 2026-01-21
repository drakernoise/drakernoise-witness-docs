# RPC API Node

We provide a public, SSL-secured RPC endpoint for the Blurt blockchain.
Optimized for low-latency requests from frontend applications (dApps).

## Connection Details

- **URL**: `https://rpc.drakernoise.com`
- **Chain ID**: `cd8d90f29ae273abec3eaa7731e25934c63eb654d55080caff2ebb7f5df6381f` (Blurt Mainnet)
- **Rate Limit**: Fair usage policy applies.
- **CORS**: Enabled for all origins (`*`).

## Usage Examples

### JavaScript (blurt.js)
```javascript
const blurt = require('@blurtfoundation/blurtjs');

blurt.api.setOptions({ url: 'https://rpc.drakernoise.com' });

blurt.api.getStartAccounts(function(err, result) {
    console.log(err, result);
});
```

### Curl
```bash
curl -X POST https://rpc.drakernoise.com \
     -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0", "method":"condenser_api.get_dynamic_global_properties", "params":[], "id":1}'
```
