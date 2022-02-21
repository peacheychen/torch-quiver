import torch
import torch_quiver as torch_qv
import torch

def test_check_memory_allocator():
    torch_qv.check_pytorch_allocator()


if __name__ == "__main__":
    test_check_memory_allocator()