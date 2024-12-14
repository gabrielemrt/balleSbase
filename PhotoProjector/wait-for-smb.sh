#!/bin/bash

MOUNT_PATH="/mnt/nas_photos"
TIMEOUT=30  # Tempo massimo in secondi per attendere il montaggio

echo "Waiting for SMB mount at ${MOUNT_PATH}..."
for i in $(seq 1 $TIMEOUT); do
    if [ -d "$MOUNT_PATH" ] && [ "$(ls -A $MOUNT_PATH)" ]; then
        echo "SMB mount available."
        exit 0
    fi
    echo "SMB mount not ready, retrying in 1 second..."
    sleep 1
done

echo "SMB mount not available after $TIMEOUT seconds."
exit 1
