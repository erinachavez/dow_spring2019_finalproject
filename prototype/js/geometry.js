let camera, scene, renderer;
let geometry, material, mesh;

const container = document.getElementById('geo_container');

init();
animate();

function init() {
  scene = new THREE.Scene();
  let width = 300;
  let height = 300;

  camera = new THREE.PerspectiveCamera(45, width/height, 0.1, 25000);
  camera.position.set(0, 0, 700);
  scene.add(camera);

  geometry = new THREE.IcosahedronGeometry(250, 0);
  material = new  THREE.MeshBasicMaterial({color: 0xcc5fcf, wireframe: true});
  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  renderer = new THREE.WebGLRenderer({alpha: 1, antialias: true});
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  renderer.render(scene, camera);
}

function animate() {
  requestAnimationFrame(animate);

  mesh.rotation.x += 0.01;
  mesh.rotation.y += 0.02;

  renderer.render(scene, camera);
}
