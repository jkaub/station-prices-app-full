function calcPointsOnCircle(lat, lon, radius, numPoints) {
  const points = [];
  const R = 6371; // Earth's radius in kilometers

  for (let i = 0; i < numPoints; i++) {
    const bearing = (360 / numPoints) * i;
    const lat2 = Math.asin(
      Math.sin(toRadians(lat)) * Math.cos(radius / R) +
        Math.cos(toRadians(lat)) *
          Math.sin(radius / R) *
          Math.cos(toRadians(bearing))
    );
    const lon2 =
      toRadians(lon) +
      Math.atan2(
        Math.sin(toRadians(bearing)) *
          Math.sin(radius / R) *
          Math.cos(toRadians(lat)),
        Math.cos(radius / R) - Math.sin(toRadians(lat)) * Math.sin(lat2)
      );
    points.push([toDegrees(lat2), toDegrees(lon2)]);
  }

  points.push(points[0]);

  return points;
}

function toRadians(degrees) {
  return (degrees * Math.PI) / 180;
}

function toDegrees(radians) {
  return (radians * 180) / Math.PI;
}

export { calcPointsOnCircle };
