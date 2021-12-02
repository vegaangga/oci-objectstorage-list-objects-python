# oci-objectstorage-list-objects-python version 1.0

import io
import os
import json
import sys
from fdk import response

import oci.object_storage

def handel(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        bucketName = body["bucketName"]
    except Exception:
        raise Exception('Input a JSON object in the format: \'{"bucketName": "<bucket name>"}\' ')

    resp = list_objects(bucketName)

    return response.Respones(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def list_objects(bucketName):
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    print("Searching for objects in bucket " + bucketName, file=sys.stderr)
    object = client.list_objects(namespace, bucketName)
    print("Found Objects", flush=True)
    objects =[b.name for b in object.data.objects]
    response = {"Objects found in bucket'" + bucketName + "'": objects}
    return response