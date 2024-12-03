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
            content = f.read()
            
        # find utilization table
        table_start = content.find('1. System Utilization')
        table_end = content.find('\n\n', table_start)
        if table_start != -1 and table_end != -1:
            table_content = content[table_start:table_end]
            
            # write to run.log
            with open(f'v{version}/run.log', 'w') as log:
                log.write(table_content + '\n\n')
            return True
    except Exception as e:
        print(f"Error extracting utilization table: {e}")
        return False

def extract_timing_summary(version):
    """extract timing summary"""
    try:
        timing_path = '_x.hw.xilinx_u250_gen3x16_xdma_4_1_202210_1/reports/link/imp/impl_1_hw_bb_locked_timing_summary_routed.rpt'
        with open(timing_path, 'r') as f:
            content = f.read()
            
        # find timing summary
        timing_start = content.find('Design Timing Summary')
        if timing_start != -1:
            lines = content[timing_start:].split('\n')
            # find the line containing WNS(ns)
            for i, line in enumerate(lines):
                if 'WNS(ns)' in line and i + 1 < len(lines):
                    timing_data = lines[i] + '\n' + lines[i+1] + '\n'
                    
                    # append to run.log
                    with open(f'v{version}/run.log', 'a') as log:
                        log.write('\nTiming Summary:\n')
                        log.write(timing_data)
                    return True
    except Exception as e:
        print(f"Error extracting timing summary: {e}")
        return False
file = [3,4]
def main():
    """main function"""
    for version in file:  # handle versions 0, 1, 2
        print(f"\nProcessing version {version}...")
        
        # cp src file and build
        if copy_and_build(version):
            # move xclbin file
            move_xclbin(version)
            
            # extract utilization table and timing summary
            extract_utilization_table(version)
            extract_timing_summary(version)
            
            print(f"Version {version} processing completed")
            os.system('make clean')
        else:
            print(f"Failed to process version {version}")

if __name__ == "__main__":
    main()
