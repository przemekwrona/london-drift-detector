### Merger
Run script to 
```shell
poetry run merge-csvs batch -d /Volumes/T7/data/delay/ -o /Volumes/T7/data/parquet/ 
```

### Plot histogram

```shell
poetry run plot-hist -i /Volumes/T7/data/parquet/2024-03-01.parquet -o /Volumes/T7/data/parquet/2024-03-01_histogram.pdf
```