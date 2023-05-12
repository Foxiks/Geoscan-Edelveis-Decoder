# Geoscan Edelveis Decoder
Real-time image decoder for Geoscan-Edelveis satellite

![1](/img/124.png)
## Usage
Now it's a release for windows. It works on AGWPE (TCP). Program launch order:
```
1. Run GUI-Decoder.exe
2. Click on "Start soundmodem"
3. Set your soundmodem to your input audio device from which the signal will be captured.
4. Click on "Start decoder" (If everything is fine, you will receive a message about successful connection.)
5. Click on "Read image" -> To display the photo in real time. The photo will also be in the folder with the decoder
```
## Build from source
1. Install modules:
```
pip install bitstring, pyinstaller
```
2. Building the program:
```
pyinstaller <params> geoscan-Decoder-UB1QBJ.py
```
3. Run decoder:
```
geoscan-Decoder-UB1QBJ -ip (ip) -p (port)
```
