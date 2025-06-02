package degreeCalc;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.structure.Edge;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.janusgraph.core.JanusGraph;
import org.janusgraph.core.JanusGraphFactory;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.time.Duration;
import java.time.Instant;

public class degreeCalc {

    public static void main(String[] args) {
        JanusGraph graph = JanusGraphFactory.open("/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr.properties");
        GraphTraversalSource g = graph.traversal();

        try {
            // 预计算总边数（大数据量时可能较慢）
            Instant start = Instant.now();

            // 预计算顶点出度
            System.out.printf("[%s] 开始计算顶点入度...%n", now());
            Map<Object, Long> inDegreeMap = new HashMap<>();
            AtomicInteger vertexCounter = new AtomicInteger(0);
            g.V().forEachRemaining(vertex -> {
                Long inDegree = g.V(vertex).inE().count().next();
                inDegreeMap.put(vertex.id(), inDegree);
                if (vertexCounter.incrementAndGet() % 10000 == 0) {
                    System.out.printf("[%s] 已处理顶点: %,d%n", now(), vertexCounter.get());
                }
            });
            System.out.printf("[%s] 顶点入度计算完成 (总计: %,d)%n%n", now(), vertexCounter.get());

            // 边遍历统计
            System.out.printf("[%s] 开始遍历边...%n", now());
            List<Double> sourceDegrees = new ArrayList<>();
            List<Double> targetDegrees = new ArrayList<>();
            AtomicInteger edgeCounter = new AtomicInteger(0);

            g.E().forEachRemaining(edge -> {
                try {
                    // 处理逻辑
                    Vertex outVertex = edge.outVertex();
                    Vertex inVertex = edge.inVertex();
                    Long srcDegree = inDegreeMap.get(outVertex.id());
                    Long tgtDegree = inDegreeMap.get(inVertex.id());

                    if (srcDegree != null && tgtDegree != null) {
                        sourceDegrees.add(srcDegree.doubleValue());
                        targetDegrees.add(tgtDegree.doubleValue());
                    }

                    // 进度打印
                    int count = edgeCounter.incrementAndGet();
                    if (count % 10000 == 0) {
                        System.out.println("已处理边: %d" + count);
                    }
                } catch (Exception e) {
                    System.err.println("处理边时发生错误: " + e.getMessage());
                }
            });

            // 最终统计
            System.out.printf("%n[%s] 边遍历完成 (总计: %,d)%n", now(), edgeCounter.get());
            System.out.printf("有效边数量: %,d%n", sourceDegrees.size());

            // 计算同配性
            System.out.printf("%n[%s] 开始计算相关系数...%n", now());
            double homophily = calculatePearsonCorrelation(sourceDegrees, targetDegrees);
            System.out.printf("[%s] Homophily Coefficient: %.4f%n", now(), homophily);

            // 总耗时
            System.out.printf("%n总耗时: %s%n", 
                Duration.between(start, Instant.now()).toString()
                    .substring(2).replaceAll("(\\d[HMS])(?!$)", "$1 ")
            );
        } finally {
            graph.close();
        }
    }

    // 获取当前时间戳 (HH:mm:ss)
    private static String now() {
        return Instant.now().atZone(java.time.ZoneId.systemDefault())
               .format(java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss"));
    }

    // 计算皮尔逊相关系数
    private static double calculatePearsonCorrelation(List<Double> x, List<Double> y) {
        if (x.size() != y.size()) {
            throw new IllegalArgumentException("Lists must be of the same size");
        }

        int n = x.size();
        double sumX = 0.0, sumY = 0.0, sumXY = 0.0, sumX2 = 0.0, sumY2 = 0.0;

        for (int i = 0; i < n; i++) {
            double xi = x.get(i);
            double yi = y.get(i);

            sumX += xi;
            sumY += yi;
            sumXY += xi * yi;
            sumX2 += xi * xi;
            sumY2 += yi * yi;
        }

        double numerator = n * sumXY - sumX * sumY;
        double denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

        return (denominator == 0) ? 0 : numerator / denominator;
    }
}