import gdown

file_id = "18ofUcldVfP_8a3brjGqZBSbzq-5F6yvt"

url = f"https://drive.google.com/uc?id={file_id}"

gdown.download(
    url=url,
    output="sales_data.csv",
    fuzzy=True,
    quiet=False
)