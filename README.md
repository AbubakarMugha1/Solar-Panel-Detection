# Solar Panel Detection for Low-Resolution Aerial Imagery

A project combining domain adaptation and super-resolution techniques to detect solar panels in low-resolution aerial imagery from developing regions like Pakistan.

## Project Structure
```
Solar-Panel-Detection/
│
├───Baseline_Implementation/
│ ├── baseline_data_preprocessing.ipynb # Preprocesses US PV01 dataset for YOLO
│ └── Baseline_Implementation.ipynb # Trains initial YOLOv5 model on US data
│
├───First_Improvement/
│ ├── create_yolo_annotations.py # Converts QGIS-extracted data to YOLO format
│ ├── First_Improvement.ipynb # Domain adaptation with Pakistani dataset
│ ├── make_annotated_images.py # Visualizes annotations for quality check
│ └── Preprocessing_Zenodo.ipynb # Processes Jiang et al. multi-res dataset
│
├───Models/
│ ├── YOLOv11_Zenodo+Local_best.pt # Final model (US pretrain + Pakistan fine-tune)
│ ├── YOLOv11_Zenodo_best.pt # US-trained model checkpoint
│ └── yolo_11_raw_local_data.pt # Pakistan-only trained model
│
├───QGIS/
│ ├── DL_Project.qgz # QGIS project file for data extraction
│ └── export_grid.py # Script to export image grids from QGIS
│
└───Second_Improvement/
  ├── Final_Results_Visualizations.txt # Displays and compares results across different models
  ├── SinSR_Upscaling.ipynb # Applies diffusion-based super-resolution
  ├── SwinIR_Upscaling.ipynb # Applies transformer-based super-resolution
  └── YOLOv11_FineTuning.ipynb # Final model training pipeline
```

## Key Features

- **Domain Adaptation**: Two-stage fine-tuning (US high-res → Pakistan low-res data)
- **Super-Resolution**: 
  - SwinIR (Transformer-based structural enhancement)
  - SinSR (Diffusion-based texture generation)
- **Custom Dataset**: 330 annotated low-res images from Lahore, Pakistan, avaialble at https://www.kaggle.com/datasets/mabubakarmughal/satellite-imagery-lahore-dha-phase-6
- **Multi-Resolution Support**: Processes imagery from 0.1m (UAV) to 0.8m (satellite)

## Methodology

Our approach combines domain adaptation and super-resolution in a 3-stage pipeline:

### 1. Baseline Model Development
**YOLOv5 Architecture**  
- Pretrained on high-resolution US imagery (PV01 subset: 0.1m UAV)
- Processes three rooftop types:  
  ✓ Flat Concrete  
  ✓ Steel Tile  
  ✓ Brick  
- Input resolution: 640×640 pixels  
- Segmentation masks converted to YOLO bounding boxes via OpenCV contour detection

### 2. Domain Adaptation
**Two-Phase Fine-Tuning**  
1. **General Feature Learning**:  
   - Trained on US dataset (20 epochs)  
   - YOLOv5m architecture for enhanced capacity  

2. **Regional Specialization**:  
   - Fine-tuned on 300 Pakistani images (10 epochs)  
   - Addresses:  
     ✓ Low-resolution (0.8m satellite)  
     ✓ Local architecture patterns  
     ✓ Environmental conditions  
   - Obtain inferences on the local dataset (30 test images)
### 3. Super-Resolution Enhancement
**Dual-Mode Upscaling**  

| Technique | Architecture       | Strength                | Scale Factor |
|-----------|--------------------|--------------------------|--------------|
| SwinIR    | Transformer-based  | Structural preservation  | 4×           |
| SinSR     | Diffusion-based    | Texture generation       | 4×           |

**Integration Flow**:  
- Input low-resolution image (Pakistan)  
- Upscale with **SwinIR**/**SinSR** to **1024×1024**  
- Detect solar panels using **fine-tuned YOLOv11l**

**Solar Panel Detection Summary**:  
## Results Comparison

| Model                                   | Raw Local Data | SinSR Upscaled Data | SwinIR Upscaled Data |
|----------------------------------------|----------------|---------------------|-----------------------|
| YOLOv11 (finetuned on local data only) | 75             | 104                 | 80                    |
| YOLOv11 (finetuned on high res + local data) | 101            | 121                 | 99                    |
