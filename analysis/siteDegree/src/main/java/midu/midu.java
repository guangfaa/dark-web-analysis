package midu;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.janusgraph.core.JanusGraph;
import org.janusgraph.core.JanusGraphFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.*;
import org.apache.tinkerpop.gremlin.process.traversal.P;
import java.nio.file.Files;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class midu {
    private static final Pattern ONION_PATTERN = Pattern.compile("([a-z0-9]{56})");

    public static void main(String[] args) {
        String configFile = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr2.properties";
        JanusGraph graph = null;
        try {
            // 打开图连接
            graph = JanusGraphFactory.open(configFile);
            GraphTraversalSource g = graph.traversal();

            // 读取sites.txt中的站点
            Set<String> uniqueSites = new HashSet<>();
            String uniqueSitesFile = "sites.txt";
            try {
                String content = new String(
                    Files.readAllBytes(Paths.get(uniqueSitesFile)),
                    StandardCharsets.UTF_8
                );
                // 使用正则表达式匹配所有56字符的onion地址
                Matcher matcher = ONION_PATTERN.matcher(content);
                while (matcher.find()) {
                    String site = matcher.group(1).toLowerCase();
                    uniqueSites.add(site);
                }
            } catch (IOException e) {
                System.err.println("读取sites.txt失败: " + e.getMessage());
                return;
            }

            System.out.println("唯一站点数量: " + uniqueSites.size());
            int count = 0;

            // 将 Set 转成 List 并打乱顺序
            List<String> siteList = new ArrayList<>(uniqueSites);
            Collections.shuffle(siteList); // 随机打乱顺序

            // 遍历每个站点，查询其出边是否指向其他unique_sites中的站点
            for (String site : siteList) {
                long pageCount = g.V().has("site", site).count().next();
                if (pageCount >= 6L){
                    try {
                        // 使用优先队列（最小堆），但自定义比较器实现降序
                        PriorityQueue<Map.Entry<String, Long>> queue = new PriorityQueue<>(
                            (e1, e2) -> e2.getValue().compareTo(e1.getValue())  // 降序排序
                        );
                        g.V().has("site", site).forEachRemaining(vertex -> {
                                String id = vertex.property("bulkLoader.vertex.id").value().toString();
                                long degree = g.V().has("bulkLoader.vertex.id", id).out().count().next();
                                // long degree = g.V().has("bulkLoader.vertex.id", id).in().count().next();
                                // long degree = g.V().has("bulkLoader.vertex.id", id).both().count().next();
                                

                                // 将数据封装为 Entry 并加入优先队列（自动排序）
                                queue.add(new AbstractMap.SimpleEntry<>(id, degree));
                            });
                        // // 将队列中的数据按顺序提取到有序的 LinkedHashMap 中
                        // Map<String, Long> sortedMap = new LinkedHashMap<>();
                        // while (!queue.isEmpty()) {
                        //     Map.Entry<String, Long> entry = queue.poll();
                        //     sortedMap.put(entry.getKey(), entry.getValue());
                        // }
                        // 取top3
                        List<Map.Entry<String, Long>> topEntries = new ArrayList<>();
                        for (int i = 0; i < 3; i++) {
                            Map.Entry<String, Long> entry = queue.poll();
                            if (entry != null) {
                                topEntries.add(entry);
                            }
                        }

                        String siteInCSV = "unknown_site";
                        if (!topEntries.isEmpty()) {
                            String page1Id = topEntries.get(0).getKey();
                            Matcher siteMatcher = ONION_PATTERN.matcher(page1Id);
                            if (siteMatcher.find()) {
                                siteInCSV = siteMatcher.group(1).toLowerCase();
                            }
                        }

                        StringJoiner csvLine = new StringJoiner(",");
                        csvLine.add(siteInCSV);
                        for (int i = 0; i < 3; i++) {
                            if (i < topEntries.size()) {
                                Map.Entry<String, Long> entry = topEntries.get(i);
                                csvLine.add(entry.getKey());
                                csvLine.add(entry.getValue().toString());
                            } else {
                                csvLine.add("");
                                csvLine.add("");
                            }
                        }

                        System.out.println(csvLine.toString());
                        count++;
                        // System.out.println("第" + count + "个站点");
                    } catch (Exception e) {
                        System.err.println("查询站点 " + site + " 时出错: " + e.getMessage());
                    }
                }
                // if (count >= 100){
                //     System.out.println("第" + count + "个站点");
                //     break;
                // }
            }
            System.out.println("第" + count + "个站点");

            // 关闭图连接
            graph.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (graph != null) {
                graph.close();
            }
        }
    }
}

            // // 筛选出数量为6的'site'并收集到列表中
            // List<Object> siteList = siteCountMap.entrySet().stream()
            //         .filter(entry -> entry.getValue() == 6)
            //         .map(Map.Entry::getKey)
            //         .collect(Collectors.toList());

            // // 检查siteList是否至少有50个元素
            // if (siteList.size() < 50) {
            //     System.out.println("Warning: siteList contains fewer than 50 sites.");
            //     // 根据实际需要选择是直接使用siteList还是采取其他措施
            // } else {
            //     // 打乱siteList顺序
            //     Collections.shuffle(siteList);

            //     // 从打乱后的列表中选择前50个site
            //     List<Object> newSiteList = siteList.subList(0, 50);

            //     // 打印新的siteList
            //     newSiteList.forEach(System.out::println);
            // }