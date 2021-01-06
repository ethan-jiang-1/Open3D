# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from numpy.lib.shape_base import apply_along_axis
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import copy
import os
import sys

python_root = os.path.dirname(os.path.dirname(__file__))

# only needed for tutorial, monkey patches visualization
sys.path.append('..')
sys.path.append(python_root)
import open3d_tutorial as o3dtut
# change to True if you want to interact with the visualization windows
o3dtut.interactive = not "CI" in os.environ

todo = ["rotated_1x", "rotated_2", "rotated_3"]

# %% [markdown]
# # Transformation
# The geometry types of Open3D have a number of transformation methods. In this tutorial we show how to use `translate`, `rotate`, `scale`, and `transform`.
# %% [markdown]
# ## Translate
# The first transformation method we want to look at is `translate`. The translate method takes a single 3D vector $t$ as input and translates all points/vertices of the geometry by this vector, $v_t = v + t$. The code below shows how the mesh is translated once in the x-directon and once in the y-direction.

# %%
if "moved_1" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_tx = copy.deepcopy(mesh).translate((1.3, 0, 0))
    mesh_ty = copy.deepcopy(mesh).translate((0, 1.3, 0))
    mesh_tz = copy.deepcopy(mesh).translate((0, 0, 1.3))
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of mesh tx: {mesh_tx.get_center()}')
    print(f'Center of mesh ty: {mesh_ty.get_center()}')
    print(f'Center of mesh tz: {mesh_tz.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_tx, mesh_ty, mesh_tz], window_name="moved_1")

# %% [markdown]
# <div class="alert alert-info">
#     
# **Note:** 
# 
# The method `get_center` returns the mean of the `TriangleMesh` vertices. That means that for a coordinate frame created at the origin `[0,0,0]`, `get_center` will return `[0.05167549 0.05167549 0.05167549]`.
# 
# </div>
# %% [markdown]
# The method takes a second argument `relative` that is by default set to `True`. If set to `False`, the center of the geometry is translated directly to the position specified in the first argument.

# %%
if "moved_2" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_mv0 = copy.deepcopy(mesh).translate((2, 2, 2), relative=False)
    mesh_mv1 = copy.deepcopy(mesh).translate((4, 4, 4), relative=False)
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of translated0 mesh: {mesh_mv0.get_center()}')
    print(f'Center of translated1 mesh: {mesh_mv1.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_mv0, mesh_mv1], windwow_name="moved_2")

# %% [markdown]
# ## Rotation
# The geometry types of Open3D can also be rotated with the method `rotate`. It takes as first argument a rotation matrix `R`. As rotations in 3D can be parametrized in a number of ways, Open3D provides convenience functions to convert from different parametrizations to rotation matrices:
# 
# - Convert from [Euler angles](https://en.wikipedia.org/wiki/Euler_angles) with `get_rotation_matrix_from_xyz` (where `xyz` can also be of the form `yzx`, `zxy`, `xzy`, `zyx`, and `yxz`)
# - Convert from [Axis-angle representation](https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation) with `get_rotation_matrix_from_axis_angle`
# - Convert from [Quaternions](https://en.wikipedia.org/wiki/Quaternion) with `get_rotation_matrix_from_quaternion`
# 
# In the code below we rotate the mesh using Euler angles.

# %%
if "rotated_1" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r0 = copy.deepcopy(mesh)
    R = mesh.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4))
    mesh_r0.rotate(R, center=(0, 0, 0))
    mesh_r0.scale(0.5, center=mesh_r0.get_center())
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of translated0 mesh: {mesh_r0.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_r0], window_name="rotated_1")

# %%
if "rotated_2" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r0 = copy.deepcopy(mesh)
    R = mesh.get_rotation_matrix_from_xyz((np.pi / 2, np.pi/3, np.pi / 4))
    print("rotated_2")
    print(R)
    mesh_r0.rotate(R, center=(0, 0, 0))
    mesh_r0.scale(0.5, center=mesh_r0.get_center())
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of translated0 mesh: {mesh_r0.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_r0], window_name="rotated_2")


def get_rt():
    import scipy.spatial
    RT = scipy.spatial.transform.Rotation

    rt = None
    if False:
        print("rt get from matrix")
        mat = mesh.get_rotation_matrix_from_xyz((np.pi / 2, np.pi/3, np.pi / 4))
        print(mat)
        rt = RT.from_matrix(mat)
    else:
        print("rt get from quat")
        quat = [0.70105738, 0.09229596, 0.56098553, 0.43045933]
        print(quat)
        rt = RT.from_quat(quat)

    print("")
    print("matrix\t", rt.as_matrix())
    # qyat [0.70105738 0.09229596 0.56098553 0.43045933]
    print("quat\t", rt.as_quat())
    print("mrp\t", rt.as_mrp())
    # print("euler", rt.as_euler())
    print("rotvec\t", rt.as_rotvec())
    return rt

if "rotated_3" in todo:
    rt = get_rt()
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r0 = copy.deepcopy(mesh)
    R = rt.as_matrix()
    print("rotated_3")
    print(R)
    mesh_r0.rotate(R, center=(0, 0, 0))
    mesh_r0.scale(0.5, center=mesh_r0.get_center())
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of translated0 mesh: {mesh_r0.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_r0], window_name="rotated_3")

# %% [markdown]
# The function `rotate` has a second argument `center` that is by default set to `True`. This indicates that the object is first centered prior to applying the rotation and then moved back to its previous center. If this argument is set to `False`, then the rotation will be applied directly, such that the whole geometry is rotated around the coordinate center. This implies that the mesh center can be changed after the rotation.

# %%
if "moved_rotated_1" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r = copy.deepcopy(mesh).translate((2, 0, 0))
    mesh_r.rotate(mesh.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 4)), center=(0, 0, 0))
    o3d.visualization.draw_geometries([mesh, mesh_r], window_name="moved_rotated_1")

# %% [markdown]
# ## Scale
# Vertices and points of Open3D geometry types can also be scaled using `scale`, $v_s = s \cdot v$. 

# %%
if "moved_scaled_1" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_s = copy.deepcopy(mesh).translate((2, 0, 0))
    mesh_s.scale(0.5, center=mesh_s.get_center())
    o3d.visualization.draw_geometries([mesh, mesh_s], window_name="moved_scaled_1")

# %% [markdown]
# The `scale` method also has a second argument `center` that is set to `True` by default. If it is set to `False`, then the object is not centered prior to scaling such that the center of the object can move due to the scaling operation.

# %%
if "moved_scaled_2" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_s = copy.deepcopy(mesh).translate((2, 1, 0))
    mesh_s.scale(0.5, center=(0, 0, 0))
    o3d.visualization.draw_geometries([mesh, mesh_s], window_name="moved_scaled_2")

# %% [markdown]
# ## General transformation
# Open3D also supports a general transformation defined by a $4\times4$ homogeneous transformation matrix using the method `transform`.

# %%
if "transformed" in todo:
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    T = np.eye(4)
    T[:3, :3] = mesh.get_rotation_matrix_from_xyz((0, np.pi / 3, np.pi / 2))
    T[0, 3] = 1
    T[1, 3] = 1.3
    print(T)
    mesh_t = copy.deepcopy(mesh).transform(T)
    o3d.visualization.draw_geometries([mesh, mesh_t], window_name="transformed")


