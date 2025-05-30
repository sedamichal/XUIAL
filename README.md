# XUIAL - Semestral paper
Operation of the thermal imaging camera WEOM WTC640-N-P-H25-30

Implementation of setup for operation

Image capturing implementation

Segmentation of captured image

## Device description
Besic documentation in [datasheet](/documents/datasheet-172-en-250303.pdf) and [drawing](/documents/drawings-177-cs-240627.pdf)

> [!NOTE]
> After device registration on vendors support page is wrong datasheet in documents, I had to find correct one on support webpage
In spec was written that device has USB-C plugin, but it was not true, there is HDMI plugin only - it means it is possible to create static images only and download them via USB interface

Camera
- SN: 20027-048-2412
- AN: WTC640-N-P-H25-30

HDMI plugin
- SN: 20009-074-2412
- AN: P-WTC-H-HDMI

## SDK/API
There is no provided SDK on support web page from vendor. But exists Weompy projects where Workswell is participating.

After installation ```pip install weompy``` you can find in your ```<env>/Lib/site-packages/weompy``` folder with documentation in Jupyter notebook

## Software
WEOM GUI application - to controll camera settings and image capturing.

CorePlayer - paid application but only for cameras with USB-C plugin, there is no option open *.wti file, camera must be connected.

## Image capturing
Image capturing is slow, about 30s. Output file *.wti has nondocumented format. It is array of numbers which represent intensity of pixels, but it is not clear how exactly calculate absolute temperature. From GUI application there is option to download pallette file, but pallette values are mapped to 256 scale. Is obvious that scale is 0 - 16378, but not clear for which temperature scale.
IMage doesn't contain radiometric data.

## Camera settings
Possibility to configure camera via weompy.