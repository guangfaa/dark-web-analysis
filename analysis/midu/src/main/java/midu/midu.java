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
    public static void main(String[] args) {
        String configFile = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr2.properties";
        JanusGraph graph = null;
        try {
            // 打开图连接
            graph = JanusGraphFactory.open(configFile);
            GraphTraversalSource g = graph.traversal();

            // 读取unique_sites.txt中的站点
            Set<String> uniqueSites = new HashSet<>();
            String uniqueSitesFile = "unique_sites.txt";
            try {
                String content = new String(
                    Files.readAllBytes(Paths.get(uniqueSitesFile)),
                    StandardCharsets.UTF_8
                );
                // 使用正则表达式匹配所有56字符的onion地址
                Pattern pattern = Pattern.compile("([a-z0-9]{56})");
                Matcher matcher = pattern.matcher(content);
                while (matcher.find()) {
                    String site = matcher.group(1).toLowerCase();
                    uniqueSites.add(site);
                }
            } catch (IOException e) {
                System.err.println("读取unique_sites.txt失败: " + e.getMessage());
                return;
            }

            System.out.println("唯一站点数量: " + uniqueSites.size());

            // 遍历每个站点，查询其出边是否指向其他unique_sites中的站点
            for (String site : uniqueSites) {
                try {
                    List<String> targets = g.V()
                        .has("site", site)
                        .out()  // 遍历出边
                        .has("site", P.within(uniqueSites))  // 目标在uniqueSites中
                        .has("site", P.neq(site))
                        .dedup()  // 去重
                        .<String>values("site")  // 获取目标站点的site属性
                        .toList();  // 转换为列表

                    // 输出连边
                    for (String target : targets) {
                        System.out.println("连接: " + site + " -> " + target);
                    }
                } catch (Exception e) {
                    System.err.println("查询站点 " + site + " 时出错: " + e.getMessage());
                }
            }

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