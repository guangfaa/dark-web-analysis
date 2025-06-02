package value;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.apache.tinkerpop.gremlin.structure.Property;
import org.janusgraph.core.JanusGraph;
import org.janusgraph.core.JanusGraphFactory;
import java.util.concurrent.atomic.AtomicLong;

public class value {
    public static void main(String[] args) {
        String configFile = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr.properties";
        long startTime = System.currentTimeMillis();

        try (JanusGraph graph = JanusGraphFactory.open(configFile)) {
            GraphTraversalSource g = graph.traversal();

            // 为 surface 和 dark 标签分别定义三个计数器
            AtomicLong surfaceZero = new AtomicLong(0);
            AtomicLong surfaceOne = new AtomicLong(0);
            AtomicLong surfaceEmpty = new AtomicLong(0);
            AtomicLong darkZero = new AtomicLong(0);
            AtomicLong darkOne = new AtomicLong(0);
            AtomicLong darkEmpty = new AtomicLong(0);

            // 遍历所有顶点
            g.V().forEachRemaining(vertex -> {
                // 获取顶点标签
                String label = vertex.label();

                // 获取 value 属性（处理属性不存在的情况）
                Object value = null;
                Property valueProp = vertex.property("value");
                if (valueProp.isPresent()) {
                    value = valueProp.value();
                    System.out.println(value);
                }

                // 判断是否为空值（包括 null 和空字符串）
                boolean isEmpty = (value == null || value.toString().isEmpty());

                // 根据标签分类统计
                if ("surface".equals(label)) {
                    if (isEmpty) {
                        surfaceEmpty.incrementAndGet();
                    } else if ("0".equals(value.toString())) {
                        surfaceZero.incrementAndGet();
                    } else if ("1".equals(value.toString())) {
                        surfaceOne.incrementAndGet();
                    }

                } else if ("dark".equals(label)) {
                    if (isEmpty) {
                        darkEmpty.incrementAndGet();
                    } else if ("0".equals(value.toString())) {
                        darkZero.incrementAndGet();
                    } else if ("1".equals(value.toString())) {
                        darkOne.incrementAndGet();
                    }
                }
            });

            // 输出统计结果
            System.out.println("===== Surface节点统计 =====");
            System.out.println("Value 0: " + surfaceZero.get());
            System.out.println("Value 1: " + surfaceOne.get());
            System.out.println("Empty  : " + surfaceEmpty.get());

            System.out.println("\n===== Dark节点统计 =====");
            System.out.println("Value 0: " + darkZero.get());
            System.out.println("Value 1: " + darkOne.get());
            System.out.println("Empty  : " + darkEmpty.get());

        } catch (Exception e) {
            e.printStackTrace();
        }

        // 计算并打印运行时间
        long endTime = System.currentTimeMillis();
        System.out.println("\nTotal running time: " + (endTime - startTime) + " ms");
    }
}