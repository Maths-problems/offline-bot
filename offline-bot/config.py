import os

OWNER_ID = int(os.getenv("OWNER_ID"))

# Anti-nuke settings
NUKE_THRESHOLD = 5       # Actions before punishment
RAID_JOIN_THRESHOLD = 6  # Rapid joins
TIME_WINDOW = 8          # Seconds for raid detection

# Server-specific storage
WHITELIST = set()        # User IDs to ignore
SERVER_SETTINGS = {}     # Guild-specific: welcome/leave channels, ticket counters, etc.
