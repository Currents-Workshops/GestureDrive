import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);
ChartJS.defaults.font.size = 18;
ChartJS.defaults.color = 'black';

const SemicircularGraph =(props) => {
  return <Radar data={props.data} />;
}
export default SemicircularGraph;
