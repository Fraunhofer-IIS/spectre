from spectre.dataset import SPECTRE

if __name__ == "__main__":
    dataset = SPECTRE(
        "path/to/data",
        int_time=1400,
        shuffle=True,
        cache_dir=None,
        clean_threshold=0.15,
        lamb_range=(450, 690),
        cache=True,
        augment=True,
    )
    dataset_l = list(dataset)
    print(len(dataset_l))
