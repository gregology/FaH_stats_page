# FaH_stats_page

```

docker build -t fah_stats_page .
docker run -d -p 8081:80 \
  --name=fah_stats_page \
  -v $PWD:/app fah_stats_page
```
