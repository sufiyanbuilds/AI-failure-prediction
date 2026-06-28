import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
  LabelList
} from "recharts";

export default function DashboardCharts({ stats }) {

  const data = [
    {
      name: "High",
      value: stats.high || 0,
      fill: "#ef4444"
    },
    {
      name: "Medium",
      value: stats.medium || 0,
      fill: "#f59e0b"
    },
    {
      name: "Low",
      value: stats.low || 0,
      fill: "#22c55e"
    }
  ];

  return (

    <div
      style={{
        width: "100%",
        height: 240,
        marginTop: "0"
      }}
    >

      <ResponsiveContainer width="100%" height="100%">

        <BarChart
          data={data}
        >

          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#334155"
          />

          <XAxis
            dataKey="name"
            stroke="#94a3b8"
          />

          <YAxis
            stroke="#94a3b8"
          />

          <Tooltip
            cursor={{ fill: "rgba(59,130,246,0.08)" }}
            contentStyle={{
              backgroundColor: "#0f172a",
              border: "1px solid #3b82f6",
              borderRadius: "12px",
              color: "#ffffff",
              boxShadow: "0 8px 20px rgba(0,0,0,0.4)"
            }}
            labelStyle={{
              color: "#38bdf8",
              fontWeight: "bold"
            }}
            itemStyle={{
              color: "#ffffff"
            }}
          />

          <Bar
            dataKey="value"
            radius={[12, 12, 0, 0]}
            animationDuration={1500}
            animationEasing="ease-out"
          >
            <LabelList
              dataKey="value"
              position="top"
              fill="#ffffff"
              fontWeight="bold"
            />

            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={entry.fill}
              />
            ))}
          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </div>

  );
}