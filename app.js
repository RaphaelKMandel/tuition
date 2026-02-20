// 2026 tuition data (from 2026tuition.csv)
const TUITION_DATA = [
  { grade: 'ECC 5 Full Days', subsidized: 14850, unsubsidized: 14850, capfrac: 0.5 },
  { grade: 'ECC 3 Full Days', subsidized: 8950, unsubsidized: 8950, capfrac: 0.5 },
  { grade: 'ECC 5 Half Days', subsidized: 9300, unsubsidized: 9300, capfrac: 0.5 },
  { grade: 'ECC 3 Half Days', subsidized: 5800, unsubsidized: 5800, capfrac: 0.5 },
  { grade: 'ECC Extended Hours', subsidized: 3400, unsubsidized: 3400, capfrac: 0.5 },
  { grade: 'Kindergarden', subsidized: 10750, unsubsidized: 17750, capfrac: 1 },
  { grade: 'Grade 1', subsidized: 11500, unsubsidized: 18000, capfrac: 1 },
  { grade: 'Grades 2-5', subsidized: 13400, unsubsidized: 18400, capfrac: 1 },
  { grade: 'Grade 6', subsidized: 16000, unsubsidized: 21000, capfrac: 1 },
  { grade: 'Grades 7-8', subsidized: 16000, unsubsidized: 21000, capfrac: 1 },
  { grade: 'Grades 9-12', subsidized: 19000, unsubsidized: 25500, capfrac: 1 }
];

const WATERFALL_THRESHOLDS = [0, 300000, 400000];
const WATERFALL_RATES = [0.15, 0.175, 0.2];

function formatDollar(x) {
  return '$' + Number(x).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatPercent(x) {
  return (Number(x) * 100).toFixed(2) + '%';
}

// WaterFall: single band based on AGI bracket; max tuition = rate * amount for that bracket
function waterfallEvaluate(amount) {
  const bands = [];
  let resultBand;
  const thresholds = WATERFALL_THRESHOLDS;
  const rates = WATERFALL_RATES;
  for (let n = 1; n < thresholds.length; n++) {
    const rate = rates[n - 1];
    const threshold = thresholds[n];
    const low = thresholds[n - 1];
    if (amount < threshold) {
      resultBand = {
        band: [low, threshold],
        rate: rate,
        diff: amount,
        value: rate * amount
      };
      bands.push(resultBand);
      break;
    }
  }
  if (!resultBand) {
    const rate = rates[rates.length - 1];
    const lastThreshold = thresholds[thresholds.length - 1];
    resultBand = {
      band: [lastThreshold],
      rate: rate,
      diff: amount,
      value: rate * amount
    };
    bands.push(resultBand);
  }
  let maxTuition = 0;
  bands.forEach(function (b) { maxTuition += b.value; });
  return {
    AGI: amount,
    bands: bands.map(function (b) {
      return {
        band: b.band,
        rate: b.rate,
        diff: b.diff,
        value: b.value
      };
    }),
    maxTuition: maxTuition
  };
}

function getTuitions(students, maxTuition, subsidized) {
  const grades = {};
  TUITION_DATA.forEach(function (row) {
    const qty = students[row.grade] || 0;
    const tuitionPer = subsidized ? row.subsidized : row.unsubsidized;
    const tuition = qty * tuitionPer;
    const qualified = row.capfrac * tuition;
    grades[row.grade] = {
      each: tuitionPer,
      count: qty,
      tuition: tuition,
      qualified: qualified
    };
  });
  let totalTuition = 0;
  let totalQualified = 0;
  Object.keys(grades).forEach(function (g) {
    totalTuition += grades[g].tuition;
    totalQualified += grades[g].qualified;
  });
  const unqualified = totalTuition - totalQualified;
  const total = unqualified + Math.min(totalQualified, maxTuition);
  return {
    grades: grades,
    totals: {
      subtotal: totalTuition,
      qualified: totalQualified,
      unqualified: unqualified,
      total: total
    }
  };
}

function getDebugLines(capData, tuitionData) {
  const lines = [];
  lines.push('At an AGI of ' + formatDollar(capData.AGI) + ':');
  capData.bands.forEach(function (band) {
    if (band.band.length === 1) {
      lines.push('    Income above ' + formatDollar(band.band[0]) + ' is considered at ' + formatPercent(band.rate) + '. You earned ' + formatDollar(band.diff) + ' resulting in ' + formatDollar(band.value));
    } else {
      lines.push('    Income between ' + formatDollar(band.band[0]) + '-' + formatDollar(band.band[1]) + ' is considered at ' + formatPercent(band.rate) + '. You earned ' + formatDollar(band.diff) + ' resulting in ' + formatDollar(band.value));
    }
  });
  lines.push('Summing the values in each band results in your maximum qualified tuition: ' + formatDollar(capData.maxTuition));
  lines.push('Your tuition expenses are as follows:');
  Object.keys(tuitionData.grades).forEach(function (grade) {
    const data = tuitionData.grades[grade];
    if (data.count > 0) {
      lines.push('    ' + data.count + ' student(s) in ' + grade + ' @ ' + formatDollar(data.each) + '/student for a sub-total of ' + formatDollar(data.tuition) + ' of which ' + formatDollar(data.qualified) + ' is qualified for the tuition cap.');
    }
  });
  lines.push('Your unqualified tuition expenses total ' + formatDollar(tuitionData.totals.unqualified) + '. These expenses are not subject to a tuition cap.');
  const qualified = tuitionData.totals.qualified;
  const maxT = capData.maxTuition;
  if (qualified > maxT) {
    lines.push('Your qualified tuition expenses total ' + formatDollar(qualified) + ', which will be capped to your max tuition: ' + formatDollar(maxT));
  } else {
    lines.push('Your qualified tuition expenses total: ' + formatDollar(qualified) + '. Because of your AGI, these tuition expenses will not be capped.');
  }
  lines.push('Summing your qualified and unqualified tuitions results in your total tuition: ' + formatDollar(tuitionData.totals.total));
  return lines;
}
