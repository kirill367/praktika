

def main():
    sorted_datas = list(VbyTdf.time).sort(key=lambda d: datetime.strptime(d, '%d.%m.%Y %H:%M'))


if __name__ == "__main__":
    main()
