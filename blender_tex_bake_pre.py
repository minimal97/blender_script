
import bpy

# 選んでるオブジェクトをテクスチャベイク準備をする。
# スクリプト終わったらRenderをCycles、Bake > Bake Type: Diffuse、Influence Colorのみでベイク。
# 終わったら
# Shading で画像つなぎなおし、UVMap切り替え

def change_image(image_name):
    # 画像を取得
    image = bpy.data.images.get(image_name)
    if image is None:
        print(f"画像 {image_name} が見つかりません")
        return

    # UV/Image Editorの領域を取得
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            # スペースを取得
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    # 画像を設定
                    space.image = image


selected_objects = bpy.context.selected_objects

obj = selected_objects[0] if selected_objects else None


# オブジェクトがメッシュであることを確認
if obj:
    if obj.type == 'MESH':
        # 新しいUVマップを作成

        uvmap = obj.data.uv_layers.new(name="NewUVMap")  # ここにUVマップ名を入力
        obj.data.uv_layers.active = uvmap
        tex = obj.data.materials[0].node_tree.nodes['Image Texture'].image
        width = tex.size[0]
        height = tex.size[1]
        print('テクスチャの幅: ', width)
        print('テクスチャの高さ: ', height)
        new_tex = bpy.data.images.new("NewTexture", width , height)
        #new_tex = bpy.data.images.new("NewTexture", width // 2 , height // 2)


        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.select_all(action='SELECT')

        bpy.ops.uv.pack_islands()

        materal = obj.data.materials[0]

        nodes = materal.node_tree.nodes

        texture = bpy.data.textures.new(name="Texture", type='IMAGE')
        texture.image = new_tex

        texture_node = nodes.new(type="ShaderNodeTexImage")
        texture_node.image = new_tex

        bpy.ops.object.mode_set(mode='OBJECT')
