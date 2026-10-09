from ftplib import FTP
import os


def download_files_ftp(accession):
    # Extract the last 3 digits from accession for the path
    # S-BIAD1658 -> 658, S-BIAD1350 -> 350
    accession_num = accession.split('-')[-1]
    last_three = accession_num[-3:]

    ftp_host = "ftp.ebi.ac.uk"
    ftp_path = f"/biostudies/fire/S-BIAD/{last_three}/{accession}/Files/"

    download_dir = os.path.expanduser("~/Downloads")
    os.makedirs(download_dir, exist_ok=True)

    print(f"Connecting to FTP server {ftp_host}...")
    print(f"FTP path: {ftp_path}\n")

    try:
        ftp = FTP(ftp_host)
        ftp.login()  # Anonymous login
        ftp.cwd(ftp_path)

        # List all files
        file_list = []
        ftp.retrlines('LIST', lambda line: file_list.append(line))

        if not file_list:
            print("No files found in the directory.")
            ftp.quit()
            return

        # Parse file information
        files_info = []
        for line in file_list:
            parts = line.split()
            if len(parts) >= 9:
                filename = ' '.join(parts[8:])
                file_size = int(parts[4])
                files_info.append((filename, file_size))

        # Sort by size
        files_info.sort(key=lambda x: x[1])

        # Display all files
        print(f"{'='*80}")
        print(f"Total files found: {len(files_info)}")
        print(f"{'='*80}\n")

        print(f"{'File Name':<60} {'Size (KB)':<15} {'Size (Bytes)':<15}")
        print(f"{'-'*60} {'-'*15} {'-'*15}")

        for fname, fsize in files_info:
            fsize_kb = fsize / 1024
            fname_display = fname if len(fname) < 60 else "..." + fname[-57:]
            print(f"{fname_display:<60} {fsize_kb:>13.2f} {fsize:>13}")

        print(f"\n{'='*80}")

        # Download the smallest file
        smallest_file, smallest_size = files_info[0]
        smallest_size_kb = smallest_size / 1024

        print(f"\nSmallest file selected for download:")
        print(f" - Name: {smallest_file}")
        print(f" - Size: {smallest_size_kb:.2f} KB ({smallest_size} bytes)")

        # Handle filename collision
        local_filepath = os.path.join(download_dir, smallest_file)
        counter = 1
        base_name, extension = os.path.splitext(smallest_file)
        original_path = local_filepath

        while os.path.exists(local_filepath):
            local_filepath = os.path.join(download_dir, f"{base_name}_{counter}{extension}")
            counter += 1

        print(f"\nDownloading to: {local_filepath}")

        with open(local_filepath, "wb") as local_file:
            ftp.retrbinary(f"RETR {smallest_file}", local_file.write)

        print(f"\n✓ Successfully downloaded {os.path.basename(local_filepath)}!")
        ftp.quit()

    except Exception as e:
        print(f"\n✗ An error occurred: {e}")

if __name__ == "__main__":
    download_files_ftp("S-BIAD1350")
    # You can also try: download_files_ftp("S-BIAD1350")
