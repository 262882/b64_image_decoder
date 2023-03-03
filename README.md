# b64_image_decoder
A python command line tool that takes base64 encoded images in .json format as an argument and outputs the processed images in a .jpeg format.

## Example of usage for single image:

Running in the working directory:
```
./decode.py test_img1.json
```

Outputs to the working directory:
```
test_img1.jpeg
```

## Example of usage for multiple images:

Running in a folder of .json files:
```
./decode.py
```

Outputs to the working directory:
```
test_img1.jpeg
test_img2.jpeg
test_img3.jpeg
```
