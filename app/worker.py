# Simple worker script placeholder (can run background tasks if needed)
import time
print('Worker started (placeholder). Sleeping...') 
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print('Worker stopped')
