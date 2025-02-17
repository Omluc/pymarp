from pymarp_binary import get_marp_path, convert_file
def main():
    marp_path = get_marp_path()
    convert_file("ma.md", "ma.pdf")
    print(marp_path)
    print("Hello from pl!")

if __name__ == "__main__":
    main()
