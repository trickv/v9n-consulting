# Privacy Policy

_Last updated: April 9, 2026_

Baby Monitor ("the app") is an open source peer-to-peer baby monitor app
that streams audio and video between two devices that you own. This
document describes what the app does and does not do with your data.

## Summary

- **No accounts.** There is no sign up, no login, and no user identifier.
- **No advertising.** The app contains no ads and no advertising SDKs.
- **No analytics.** The app does not track usage, crashes, or behavior.
- **No data sale or sharing.** Nothing about you or your device is sold,
  shared, or transferred to third parties.
- **No data storage.** Audio and video are not recorded by the app and
  are not stored anywhere by us.
- **Source available.** The full source code is published at
  https://github.com/trickv/baby-monitor and you can verify these claims.

## What the app accesses

### Camera and microphone

The app needs camera and microphone permissions on the "baby" device so
it can capture audio and video and stream them to the "parent" device.

The audio and video stream is sent **directly between the two devices**
over a peer-to-peer WebRTC connection. The stream is not recorded, is
not stored on any server, and is not accessible to anyone other than
the two devices in the active session.

### Local network and internet

The app uses your local network and internet connection to establish a
connection between the baby and parent devices. This involves a small
amount of connection-setup data ("signaling") passing through a
signaling server so that the two devices can find each other and
negotiate a direct connection.

The signaling data contains technical information necessary to set up
the WebRTC session (network candidates, connection parameters). It
does not contain audio, video, or any personal information about you.
The signaling server does not retain this data beyond the lifetime of
the connection.

## What the app does not do

- The app does not collect, store, or transmit your name, email, phone
  number, location, contacts, photos, files, or any other personal
  information.
- The app does not record audio or video.
- The app does not access, read, or modify files on your device outside
  of what the operating system requires for normal app operation.
- The app does not contain third-party advertising or analytics SDKs.
- The app does not use device identifiers for tracking.

## Children

This app is intended for use by **adults** (parents and caregivers) to
monitor an infant or child in their care. The app is not designed for
use by children and does not knowingly collect any information from
children. The presence of a child in the camera frame is not "data
collection" in the legal sense — the video is streamed only to the
other device the user controls, and is not retained.

## Changes to this policy

Any changes to this policy will be published to this same document in
the project repository. The "Last updated" date at the top will reflect
the most recent change.

## Contact

For questions about this privacy policy or the app, open an issue at
https://github.com/trickv/baby-monitor/issues.
