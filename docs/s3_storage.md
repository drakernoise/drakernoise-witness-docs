# Decentralized Storage (IS3)

We afford an S3-compatible object storage service powered by **MinIO**. 
This service allows developers to host static assets (images, JSON metadata) in a decentralized manner, backed by Drakernoise infrastructure.

## Connection Details

| Parameter | Value |
| :--- | :--- |
| **Endpoint** | `https://images.drakernoise.com` |
| **Region** | `us-east-1` (Default) |
| **SSL** | Yes (Required) |


> [!NOTE]
> You can verify the service status by visiting **[https://images.drakernoise.com](https://images.drakernoise.com)** in your browser to see our Developer Landing Page.

## Access Policy
Access is currently **Invite Only** for active Blurt developers.
Contact **@drakernoise** on Discord/Blurt to request your `Access Key` and `Secret Key`.

## Integration

### Python (boto3)
```python
import boto3
from botocore.client import Config

s3 = boto3.client('s3',
    endpoint_url='https://images.drakernoise.com',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    config=Config(signature_version='s3v4')
)

# Upload image
s3.upload_file('local_image.jpg', 'public-assets', 'remote_image.jpg')
print("Url: https://images.drakernoise.com/public-assets/remote_image.jpg")
```

### JavaScript (AWS SDK v3)
```javascript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({
    region: "us-east-1",
    endpoint: "https://images.drakernoise.com",
    credentials: {
        accessKeyId: "YOUR_ACCESS_KEY",
        secretAccessKey: "YOUR_SECRET_KEY"
    }
});
```
