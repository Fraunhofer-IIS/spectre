from spectre.dataset import SPECTRE

if __name__ == "__main__":
    dataset = SPECTRE("/Users/wgj/SPECTRE/spectre-public")
    dataset_l = list(dataset)
    print(len(dataset_l))
