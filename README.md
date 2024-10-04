# Mimicker

CLI tool for structurizing flat collection of photos based on structurized previews.

Copy directory tree with replacing previews with hi-quality images

## Requirements

This is a python3 project that don't require any other external packages - purely based on standard library. 

## Installation

1. Install python3 in your system.
1. Clone the repository.

   ```sh
   git clone https://github.com/izikeros/mimicker
   ```

## Usage
```
mimi.py [-h] [--sel-only] [--level-up-sel] [--verbose] [--force] prev_dir hq_flat_dir hq_struct_dir

positional arguments:
  prev_dir            Directory with previews structurized into subdirectories
  hq_flat_dir         Directory with multimedia in high quality, flat structure
  hq_struct_dir       Directory with multimedia in high quality, with mirrored structure

optional arguments:
  -h, --help          show this help message and exit
  --sel-only, -s      Keep only content of "sel" subdirectories
  --level-up-sel, -l  Move content of sel folder
  --verbose, -v       Display more information on what is happening during the operation.
  --force, -f         Force removing of the output directory if exists.
```
## My use case

This is a helper tool to be used in my photography workflow for applying structure I have added to previews to the high quality exports living in the flat directory.

Sometimes I do photo selection being away from my workstation and for such cases I generate miniatures (previews). Later, I orgranize e.g. photos from the big trip into folders related to different trip stages. And inside stages I perform the selection of photos I would like to include into presentation (or other form of delivery).
In each subdirectory I create `sel` or `selected` folder and move or copy pictures there.
The outcome of the selection is structurized directory but with the low quality previews. What I would like achieve is the same structure but containing high quality photos taken from flat directory with exported, postprocessed photos. Here comes this tool - scans structure of stucturized previews, create the same structure but with the HQ photos from the flat folder with all HQ photos.

## Related Projects

Let me know if you aware of tools providing the same functionality.

## License

[MIT](LICENSE) © [Krystian Safjan](https://safjan.com/).
---
