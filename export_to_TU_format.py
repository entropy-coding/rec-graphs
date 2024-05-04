import os
from pathlib import Path

from rec.datasets import AVAILABLE_DATASETS, load_dataset

categories = [
    ("Large social networks", AVAILABLE_DATASETS[:4]),
    ("Large non-social networks", AVAILABLE_DATASETS[4:])
]

names = {
    "youtube": "YouTube",
    "foursquare": "Foursquare",
    "digg": "Digg",
    "gowalla": "Gowalla",
    "skitter": "Skitter",
    "dblp": "DBLP"
}


def main():
    out_dir = Path(os.environ.get("EXPORT_DIR"))
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "datasets.md").open("w") as index:
        index.write("# REC graph data\n")

        for category_name, datasets in categories:
            index.write(f"""
## {category_name}

| **Name**    | **Source** | **Statistics** |           |              | **Labels/Attributes** |               |               |              |            |              | **Download (ZIP)**                                                                  |
|-------------|------------|----------------|-----------|--------------|-----------------------|:-------------:|:-------------:|:------------:|:----------:|:------------:|-------------------------------------------------------------------------------------|
|             |            | *Graphs*       | *Classes* | *Avg. Nodes* | *Avg. Edges*          | *Node Labels* | *Edge Labels* | *Node Attr.* | *Geometry* | *Edge Attr.* |                                                                                     |
| ---         | ---        | ---            | ---       | ---          | ---                   |     :---:     |     :---:     |     ---      |    ---     |     ---      | ---                                                                                 |
""")

            for dataset in datasets:
                d = load_dataset(dataset, -1)
                name = names[dataset]
                index.write(
                    f"|**{name}**|[1]|1|--|{d.num_nodes}|{d.num_edges}|--|--|--|--|--|[{name}](https://github.com/entropy-coding/rec-graphs/raw/main/datasets/{name}.zip)|\n")

                name_dir = out_dir / name
                name_dir.mkdir(parents=True, exist_ok=True)
                edges = list(sorted(d.sorted_edge_list + [[v, u] for (u, v) in d.sorted_edge_list]))
                assert len(edges) == len(set(map(tuple, edges)))
                assert len(edges) == 2 * d.num_edges

                with (name_dir / f"{name}_A.txt").open("w") as f:
                    for (u, v) in edges:
                        f.write(f"{u + 1}, {v + 1}\n")
                with (name_dir / f"{name}_graph_indicator.txt").open("w") as f:
                    for i in range(d.num_nodes):
                        f.write(f"{1}\n")


if __name__ == "__main__":
    main()
