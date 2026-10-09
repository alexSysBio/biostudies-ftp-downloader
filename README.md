# biostudies-ftp-downloader

A minimal, dependency-free Python script for exploring and sampling datasets from [EBI BioStudies](https://www.ebi.ac.uk/biostudies/) — including the [BioImage Archive](https://www.ebi.ac.uk/bioimage-archive/) (`S-BIAD` accessions) — over anonymous FTP.

Given an accession (e.g., `S-BIAD1350`), the script:

1. Connects anonymously to `ftp.ebi.ac.uk` and resolves the dataset's file directory.
2. Lists every file in the dataset and prints a table of names and sizes, sorted by size.
3. Downloads the smallest file to `~/Downloads` — a quick way to sample a dataset (which can be terabytes of imaging data) before committing to a full download. Existing local files are never overwritten; a numeric suffix is appended instead.

## Usage

No dependencies beyond the Python 3 standard library.

```bash
python download_biostudies_ftp.py
```

Edit the accession in the `__main__` block at the bottom of the script, or import the function:

```python
from download_biostudies_ftp import download_files_ftp

download_files_ftp("S-BIAD1658")
```

## Notes

- The FTP directory layout follows the BioStudies FIRE storage convention: the parent folder is the last three digits of the accession number, i.e., `S-BIAD1658` is stored under `/biostudies/fire/S-BIAD/658/S-BIAD1658/Files/`.
- Only the smallest file is downloaded by default; adapt the end of `download_files_ftp` to fetch more (or all) files.

## License

This project is licensed under the [MIT License](LICENSE).

Author: Alexandros Papagiannakis
