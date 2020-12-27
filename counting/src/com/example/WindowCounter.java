package com.example;

import java.util.LinkedList;
import java.util.List;

public class WindowCounter {
  int width;
  List<Bucket> buckets;
  long oldestTsDeciMillis;

  public WindowCounter(int widthDeciMillis) {
    width = widthDeciMillis;
    buckets = new LinkedList<>();
  }

  public void add(long tsDeciMillis) {
    expire(tsDeciMillis);
    int ts = (int) tsDeciMillis % width;
    buckets.add(0, new Bucket(ts));
    merge();
  }


  public int count(long tsDeciMillis) {
    expire(tsDeciMillis);
    int sum = 0;
    if (buckets.isEmpty()) {
      oldestTsDeciMillis = tsDeciMillis;
      return 0;
    }
    sum = buckets.get(0).count;
    for (int i = 1; i < buckets.size() - 1; i ++) {
      sum += buckets.get(i).count;
    }
    sum += buckets.get(buckets.size() - 1).count / 2;
    return sum;
  }

  public void cleanup(int tsDeciMillis) {
    expire(tsDeciMillis);
  }

  public void dump() {
    for (Bucket bucket : buckets) {
      System.out.print("[" + bucket.ts + ", " + bucket.count + "] ");
    }
    System.out.println();
  }

  private int ts(long tsDeciMillis) {
    return (int) tsDeciMillis % width;
  }

  private int tsDiff(int ts1, int ts2) {
    return ModuloInteger.mod(ts1 - ts2, width);
  }

  private void expire(long tsDeciMillis) {
    if (buckets.isEmpty()) {
      return;
    }
    if (tsDeciMillis - oldestTsDeciMillis > width) {
      Bucket bucket = buckets.get(buckets.size() - 1);
      System.out.println("Removing oldest bucket with ts: " + bucket.ts + " and count: " + bucket.count);
      if (buckets.size() >= 2) {
        oldestTsDeciMillis += tsDiff(buckets.get(buckets.size() - 2).ts, buckets.get(buckets.size() - 1).ts);
      }
      buckets.remove(buckets.size() - 1);
      dump();
    }
  }

  private void merge() {
    for (int i = 0; i < buckets.size(); i++) {
      if (i + 2 < buckets.size()
          && buckets.get(i).count == buckets.get(i + 1).count
          && buckets.get(i + 1).count == buckets.get(i + 2).count) {
        System.out.println("Merging buckets " + i + " and " + (i + 1));
        buckets.get(i + 1).count *= 2;
        if (i + 2 == buckets.size() - 1) {
          oldestTsDeciMillis += tsDiff(buckets.get(buckets.size() - 2).ts, buckets.get(buckets.size() - 1).ts);
        }
        buckets.remove(i + 2);
      }
    }
  }

  private static class Bucket {
    public Bucket(int ts) {
      this.ts = ts;
      this.count = 1;
    }
    int ts;
    int count;
  }
}
