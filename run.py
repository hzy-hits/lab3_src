import os
import shutil
import re

def copy_and_build(version):
    """copy src file and build"""
    src_file = f'src/mm_v{version}.cpp'
    dst_file = 'src/mm.cpp'
    try:
        shutil.copy2(src_file, dst_file)
        os.system('make all')
        return True
    except Exception as e:
        print(f"Error during copy and build: {e}")
        return False

def move_xclbin(version):
    """move xclbin file"""
    try:
        # create version directory
        os.makedirs(f'v{version}', exist_ok=True)
        
        # move xclbin files
        build_dir = 'build_dir.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1'
        if os.path.exists(build_dir):
            for file in os.listdir(build_dir):
                if file.endswith('.xclbin'):
                    src_path = os.path.join(build_dir, file)
                    dst_path = os.path.join(f'v{version}', file)
                    shutil.move(src_path, dst_path)
                    print(f"Moved {file} to v{version}/")
        else:
            print(f"Build directory {build_dir} not found")
    except Exception as e:
        print(f"Error moving xclbin files: {e}")

def extract_utilization_table(version):
    """extract utilization table"""
    try:
        report_path = '_x.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1/reports/link/imp/impl_1_kernel_util_routed.rpt'
        with open(report_path, 'r') as f:
            lines = f.readlines()
            
        # find utilization table
        last_50_lines = lines[-50:]
            
            # write to run.log
        with open(f'v{version}/run.log', 'w') as log:
            log.writelines(last_50_lines)
        return True
    except Exception as e:
        print(f"Error extracting utilization table: {e}")
        return False

def extract_timing_summary(version):
    """Extract lines 135 to 145 from the timing summary report"""
    try:
        timing_path = '_x.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1/reports/link/imp/impl_1_hw_bb_locked_timing_summary_routed.rpt'
        

        with open(timing_path, 'r') as f:
            lines = f.readlines()
        

        selected_lines = lines[134:145]  
        
        os.makedirs(f'v{version}', exist_ok=True)
        

        with open(f'v{version}/run.log', 'a') as log:
            log.write('\nTiming Summary (Lines 135-145):\n')
            log.writelines(selected_lines)
        
        print(f"Successfully extracted lines 135-145 to v{version}/run.log")
        return True
    except Exception as e:
        print(f"Error extracting timing summary: {e}")
        return False
def copy_reports(version):
    """Copy report files to version directory"""
    try:
        # Create version directory if it doesn't exist
        os.makedirs(f'v{version}', exist_ok=True)
        
        # Define report files to copy
        report_files = [
            '_x.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1/reports/link/imp/impl_1_kernel_util_routed.rpt',
            '_x.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1/reports/link/imp/impl_1_hw_bb_locked_timing_summary_routed.rpt'
        ]
        
        for report in report_files:
            if os.path.isfile(report):
                dst_report = os.path.join(f'v{version}', os.path.basename(report))
                shutil.copy2(report, dst_report)
                print(f"Copied {report} to {dst_report}")
            else:
                print(f"Report file {report} not found.")
    except Exception as e:
        print(f"Error copying report files: {e}")
file = [4]

def main():
    """main function"""
    for version in file:  # handle versions 0, 1, 2
        print(f"\nProcessing version {version}...")
        
        # cp src file and build
        if copy_and_build(version):
            # move xclbin file
            move_xclbin(version)
            copy_reports(version)
            # extract utilization table and timing summary
            extract_utilization_table(version)
            extract_timing_summary(version)
            
            print(f"Version {version} processing completed")
            os.system('make clean')
        else:
            print(f"Failed to process version {version}")

if __name__ == "__main__":
    main()
